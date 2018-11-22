defmodule WalletWeb.UssdController do
  use WalletWeb, :controller
  require Logger

  action_fallback(WalletWeb.FallbackController)

  def index(conn, %{"text" => "", "phoneNumber" => phone}) do
    Wallet.create_user_if_not_exists(phone: phone)

    menu = """
    CON What would you like to do?
    1. Check balance
    2. Transfer
    3. Approve transfer with OTP
    """

    send_resp(conn, :ok, menu)
  end

  def index(conn, %{"text" => "1", "phoneNumber" => phone}) do
    balance = Wallet.get_available_balance(phone: phone, term: :string)

    response = "END Your account balance is NGN #{balance}"

    send_resp(conn, :ok, response)
  end

  def index(conn, %{"text" => "2", "phoneNumber" => _}) do
    response = "CON Enter phone number to transfer to:"

    send_resp(conn, :ok, response)
  end

  def index(%{assigns: %{level: 2}} = conn, %{
        "text" => "2*" <> phone_to,
        "phoneNumber" => phone_from
      }) do
    Wallet.create_user_if_not_exists(phone: phone_to)

    current_balance = Wallet.get_available_balance(phone: phone_from, term: :string)

    response = "CON Enter amount to transfer (current balance is NGN #{current_balance}):"

    send_resp(conn, :ok, response)
  end

  def index(%{assigns: %{level: 3}} = conn, %{"text" => "2*" <> str, "phoneNumber" => phone_from}) do
    response =
      case String.split(str, "*", trim: true) do
        [phone_to, amount] ->
          # Remove commas from amount, if any, and convert to integer
          amount =
            amount
            |> String.replace(",", "")
            |> String.to_integer()

          case Wallet.transfer(from: phone_from, to: phone_to, amount: amount) do
            {:error, :insufficient_balance} ->
              "END Insufficient balance"

            {:ok, _} ->
              "END Transfer pending. Use the OTP sent to you to approve"
          end

        _ ->
          "END Transaction terminated"
      end

    send_resp(conn, :ok, response)
  end

  def index(conn, %{"text" => "3", "phoneNumber" => _}) do
    response = "CON Enter OTP to approve transfer:"

    send_resp(conn, :ok, response)
  end

  def index(%{assigns: %{level: 2}} = conn, %{"text" => "3*" <> otp, "phoneNumber" => _}) do
    response =
      case Wallet.approve_transfer(otp) do
        {:error, :not_found} -> "END Invalid OTP"
        {:error, :recipient_not_found} -> "END Invalid recipient"
        {:ok, _} -> "END Transfer approved"
      end

    send_resp(conn, :ok, response)
  end

  # The first port of call for the controller
  def action(conn, _) do
    Logger.info("Received params: #{inspect(conn.params)}")

    text_parts =
      conn.params
      |> Map.get("text")
      |> String.split("*", trim: true)

    level =
      case text_parts do
        [""] -> 0
        _ -> length(text_parts)
      end

    conn = assign(conn, :level, level)

    apply(__MODULE__, action_name(conn), [conn, conn.params])
  end
end
