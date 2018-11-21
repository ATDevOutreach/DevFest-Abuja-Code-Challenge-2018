defmodule Wallet.PendingTransactionsCache do
  use GenServer

  def start_link do
    GenServer.start_link(__MODULE__, %{table_name: :pending}, name: :pending)
  end

  def start_link(_), do: start_link()

  def init(state) do
    send(self(), :init)
    {:ok, state}
  end

  def handle_info(:init, %{table_name: table_name} = state) do
    table_opts = [:named_table, :set, :public]
    :ets.new(table_name, table_opts)

    {:noreply, state}
  end

  def handle_call({:get, otp: otp}, _, %{table_name: table_name} = state) do
    case :ets.lookup(table_name, otp) do
      [] ->
        {:reply, {:error, :not_found}, state}

      [{_, record}] ->
        {:reply, {:ok, record}, state}
    end
  end

  def handle_cast({:store, %{otp: otp} = record}, %{table_name: table_name} = state) do
    :ets.insert(table_name, {otp, record})
    {:noreply, state}
  end

  def handle_cast({:delete, otp: otp}, %{table_name: table_name} = state) do
    :ets.delete(table_name, otp)
    {:noreply, state}
  end
end
