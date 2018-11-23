#!/bin/bash
mix do ecto.create, ecto.migrate, phx.server
