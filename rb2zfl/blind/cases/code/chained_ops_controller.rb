class TextPipelineController < ApplicationController
  def transform
    result = params[:input].to_s
    params.fetch(:steps, []).each do |step|
      op = step[:op]
      arg = step[:arg]
      result = arg.nil? ? result.public_send(op) : result.public_send(op, arg)
    end
    render json: { output: result.to_s }
  end
end
