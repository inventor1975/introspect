class Support::ConsoleController < ApplicationController
  before_action :require_console_feature

  def run
    snippet = params[:snippet].to_s
    output = binding.eval(snippet)
    render plain: output.inspect
  end

  private

  def require_console_feature
    head :not_found unless Flipper.enabled?(:support_console)
  end
end
