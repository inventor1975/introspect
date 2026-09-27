require_relative 'lib/markup_snippets'

class DeploymentStatusController < ApplicationController
  def show
    chip = MarkupSnippets.status_chip(params[:status], 'info')
    render html: MarkupSnippets.section('Deployment', "<p>Current state: #{chip}</p>").html_safe
  end
end
