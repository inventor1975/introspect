class NotesController < ApplicationController
  def quick_preview
    render inline: "<div class='note'><%= raw params[:note] %></div>", layout: false
  end
end
