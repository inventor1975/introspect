require "sinatra"

get "/stores/near" do
  zip = params[:zip]
  stores = Store.where("postal_code = ?", zip).limit(10)
  stores.to_json
end
