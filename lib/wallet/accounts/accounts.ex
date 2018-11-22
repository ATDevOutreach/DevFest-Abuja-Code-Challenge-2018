defmodule Wallet.Accounts do
  @moduledoc """
  The Accounts context.
  """

  import Ecto.Query, warn: false
  alias Wallet.Repo

  alias Wallet.Accounts.User

  def list_users do
    Repo.all(User)
  end

  def get_user(id: id), do: Repo.get(User, id)
  def get_user(phone: phone), do: Repo.get_by(User, phone: phone)

  def create_user(attrs \\ %{}) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end

  def delete_user(%User{} = user) do
    Repo.delete(user)
  end
end
