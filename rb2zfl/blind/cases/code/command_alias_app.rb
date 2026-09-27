require "sinatra/base"

class ChatOps < Sinatra::Base
  ALIASES = {
    "st" => "status",
    "dep" => "deploy_status",
    "v" => "version"
  }.freeze

  helpers do
    def status
      "all systems nominal"
    end

    def deploy_status
      "last deploy 12m ago"
    end

    def version
      "3.4.1"
    end
  end

  post "/command" do
    name = ALIASES.fetch(params[:cmd], params[:cmd])
    args = params[:args].to_s.split(",")
    send(name, *args).to_s
  end
end
