require "sinatra"

FORBIDDEN = /\b(system|exec|spawn|fork|File|IO|Dir|open|require|load|`)/

post "/formula" do
  formula = params[:formula].to_s
  if formula =~ FORBIDDEN
    halt 422, "formula contains forbidden words"
  end
  eval(formula).to_s
end
