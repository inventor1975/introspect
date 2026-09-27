class GreetingCardsController < ApplicationController
  helper_method :greeting

  def greeting(name)
    "Happy holidays, #{name}!"
  end

  def show
    recipient = params[:name].to_s
    message = eval("greeting(#{recipient.inspect})")
    render plain: message
  end
end
