require "sinatra/base"
require "json"

class JobControl < Sinatra::Base
  PERMITTED = %w[pause resume retry].freeze

  class JobHandle
    def initialize(id) = @id = id
    def pause = "paused #{@id}"
    def resume = "resumed #{@id}"
    def retry = "retrying #{@id}"
  end

  post "/jobs/:id/:action" do
    action = params[:action]
    halt 403, "action not allowed" unless PERMITTED.include?(action)
    job = JobHandle.new(params[:id].to_i)
    job.send(action)
  end
end
