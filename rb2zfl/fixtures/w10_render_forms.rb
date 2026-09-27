class PreviewController < ApplicationController
  def show
    render inline: "<p>#{params[:t]}</p>" # request text compiled as ERB
  end
  def rich
    render html: helpers.sanitize(params[:b], attributes: %w[href onclick]) # onclick allowed
  end
  def plain
    render html: helpers.sanitize(params[:c])
  end
end
