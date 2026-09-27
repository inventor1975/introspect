class NotesController < ApplicationController
  NOTES_DIR = Rails.root.join("data", "notes").to_s

  def update
    slug = params[:slug].to_s.strip
    body = params[:body].to_s

    File.write(File.join(NOTES_DIR, "#{slug}.md"), body)
    redirect_to note_path(slug), notice: "Saved"
  end
end
