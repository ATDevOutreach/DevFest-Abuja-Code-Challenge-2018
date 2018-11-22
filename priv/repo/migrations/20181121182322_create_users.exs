defmodule Wallet.Repo.Migrations.CreateUsers do
  use Ecto.Migration

  def change do
    create table(:users) do
      add(:name, :string)
      add(:phone, :string)
      add(:balance, :integer)

      timestamps()
    end

    create(unique_index(:users, [:phone]))
  end
end
