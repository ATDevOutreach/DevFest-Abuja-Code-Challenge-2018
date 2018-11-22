defmodule Wallet.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field(:name, :string)
    field(:phone, :string)
    field(:balance, :integer)

    timestamps()
  end

  @doc false
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:name, :phone, :balance])
    |> validate_required([:name, :phone, :balance])
    |> unique_constraint(:phone)
  end
end
