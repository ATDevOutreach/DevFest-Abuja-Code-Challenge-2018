defmodule WalletWeb.Router do
  use WalletWeb, :router

  pipeline :api do
    plug(:accepts, ["json"])
  end

  scope "/", WalletWeb do
    pipe_through(:api)

    post("/ussd_handler", UssdController, :index)
  end
end
