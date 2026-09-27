require_relative 'lib/feedback_entry'

class FeedbackController < ApplicationController
  def preview
    entry = FeedbackEntry.new(author: current_author_name, message: params[:message])
    render html: entry.rendered.html_safe
  end

  private

  def current_author_name
    'Anonymous'
  end
end
