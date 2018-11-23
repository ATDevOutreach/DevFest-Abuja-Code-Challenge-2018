defmodule Wallet do
  @moduledoc """
  Wallet keeps the contexts that define your domain
  and business logic.

  Contexts are also responsible for managing your data, regardless
  if it comes from the database, an external API or others.
  """
  @cache_name :pending
  require Logger

  def create_user_if_not_exists(phone: phone) do
    case get_user(phone: phone) do
      nil ->
        create_user(%{phone: phone, name: phone})

      user ->
        {:ok, user}
    end
  end

  def create_user(%{phone: _, name: _} = attrs) do
    # Initialize account with N50,000
    attrs = Map.put(attrs, :balance, 50_000_00)
    Wallet.Accounts.create_user(attrs)
  end

  def get_user(phone: phone) do
    Wallet.Accounts.get_user(phone: phone)
  end

  def get_user(id: id) do
    Wallet.Accounts.get_user(id: id)
  end

  def get_available_balance(phone: phone, term: term) do
    {:ok, %{balance: balance}} = create_user_if_not_exists(phone: phone)

    format_amount(amount: balance, term: term)
  end

  defp format_amount(amount: amount, term: term) do
    # Convert from kobo to naira
    amount =
      case amount do
        0 ->
          0

        _ ->
          amount / 100
      end

    case term do
      :string ->
        :erlang.float_to_binary(amount, decimals: 2)

      :number ->
        amount
    end
  end

  def transfer(from: from_phone, to: to_phone, amount: amount) do
    # Convert to kobo for internal use
    kobo_amount = amount * 100
    %{id: from_id, balance: from_balance} = from = get_user(phone: from_phone)
    %{id: to_id} = get_user(phone: to_phone)

    case from_balance >= kobo_amount do
      true ->
        otp = :rand.uniform(999_999)

        GenServer.cast(
          @cache_name,
          {:store, %{otp: otp, from: from_id, to: to_id, amount: kobo_amount}}
        )

        Wallet.Accounts.update_user(from, %{balance: from_balance - kobo_amount})
        # Send otp via sms
        msg = "Use #{otp} to approve your transfer of NGN #{amount} to #{to_phone}"
        Logger.info("Send '#{msg}' from #{from_phone}")

        sms_params = %{
          to: from_phone,
          msg: msg
        }

        spawn(fn -> Wallet.Request.send(sms_params) end)

        {:ok, otp}

      false ->
        {:error, :insufficient_balance}
    end
  end

  def approve_transfer(otp) do
    otp =
      case is_integer(otp) do
        true -> otp
        false -> String.to_integer(otp)
      end

    case GenServer.call(@cache_name, {:get, otp: otp}) do
      {:error, :not_found} = err ->
        err

      {:ok, %{otp: otp, to: to_id, from: from_id, amount: amount}} ->
        case get_user(id: to_id) do
          nil ->
            {:error, :recipient_not_found}

          %{balance: to_balance} = to ->
            %{phone: from_phone} = get_user(id: from_id)

            {:ok, %{phone: to_phone}} =
              Wallet.Accounts.update_user(to, %{balance: to_balance + amount})

            GenServer.cast(@cache_name, {:delete, otp: otp})
            # Inform recipient of transfer
            amount = format_amount(amount: amount, term: :string)
            msg = "Received NGN #{amount} from #{from_phone}"
            Logger.info("Send '#{msg}' to #{to_phone}")

            sms_params = %{
              to: to_phone,
              msg: msg
            }

            spawn(fn -> Wallet.Request.send(sms_params) end)
            {:ok, :successful}
        end
    end
  end
end
