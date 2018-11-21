defmodule WalletWeb.Router do
  use WalletWeb, :router

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/api", WalletWeb do
    pipe_through :api
  end
end
