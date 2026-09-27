class TopicsController < ApplicationController
  SLUG = /^[a-z0-9-]+$/

  def show
    slug = params[:slug].to_s
    unless slug.match?(SLUG)
      return render html: '<p>Invalid topic</p>'.html_safe, status: :bad_request
    end
    render html: "<h1>Topic: #{slug}</h1>".html_safe
  end
end
