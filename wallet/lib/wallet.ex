defmodule Wallet do
  @moduledoc """
  Wallet keeps the contexts that define your domain
  and business logic.

  Contexts are also responsible for managing your data, regardless
  if it comes from the database, an external API or others.
  """
  @cache_name :pending

  def create_user_if_not_exists(phone: phone) do
    case get_user(phone: phone) do
      {:ok, _} = resp ->
        resp

      {:error, _} ->
        create_user(%{phone: phone, name: phone})
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

  def get_available_balance(phone: phone) do
    {:ok, %{balance: balance}} = create_user_if_not_exists(phone: phone)

    # Convert from kobo to naira
    balance / 100
  end

  def transfer(from: from_phone, to: to_phone, amount: amount) do
    # Convert to kobo for internal use
    amount = amount * 100
    {:ok, %{id: from_id, balance: from_balance} = from} = get_user(phone: from_phone)
    {:ok, %{id: to_id}} = get_user(phone: to_phone)

    case from_balance >= amount do
      true ->
        otp = :rand.uniform(999_999)

        GenServer.cast(
          @cache_name,
          {:store, %{otp: otp, from: from_id, to: to_id, amount: amount}}
        )

        Wallet.Accounts.update_user(from, %{balance: from_balance - amount})
        {:ok, otp}

      false ->
        {:error, :insufficient_balance}
    end
  end

  def approve_transfer(otp) do
    case GenServer.call(@cache_name, {:get, otp: otp}) do
      {:error, :not_found} = err ->
        err

      {:ok, %{otp: otp, to: to_id, amount: amount}} ->
        case get_user(id: to_id) do
          {:error, _} ->
            {:error, :recipient_not_found}

          {:ok, %{balance: to_balance} = to} ->
            Wallet.Accounts.update_user(to, %{balance: to_balance + amount})
            GenServer.cast(@cache_name, {:delete, otp: otp})
            {:ok, :successful}
        end
    end
  end
end
