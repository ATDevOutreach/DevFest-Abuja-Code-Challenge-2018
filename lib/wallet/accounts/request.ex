defmodule Wallet.Request do
  require Logger

  @at_api_url Application.get_env(:wallet, :at)[:url]
  @at_api_key Application.get_env(:wallet, :at)[:api_key]
  @at_username Application.get_env(:wallet, :at)[:username]
  @request_timeout 10_000
  @err_resp "ERR_NO_RESP"

  def send(data) do
    data = Map.put(data, :username, @at_username)
    data_str = Jason.encode!(data)

    headers = [
      apiKey: @at_api_key,
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json"
    ]

    response =
      HTTPotion.post(@at_api_url, body: data_str, headers: headers, timeout: @request_timeout)

    case HTTPotion.Response.success?(response) do
      true ->
        Logger.info("Response -> #{inspect(response.body)}")

        case response.body do
          "null" ->
            {:error, @err_resp}

          body ->
            {:ok, Jason.decode!(body)}
        end

      false ->
        response = Map.from_struct(response)
        Logger.error("Request failed because -> #{inspect(response)}")
        {:error, @err_resp}
    end
  end
end
