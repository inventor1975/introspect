class ReleaseNotesController < ApplicationController
  def show
    requested = params[:version].to_s
    notes = File.read(Rails.root.join("CHANGELOG.md"))
    section = extract_section(notes, requested)

    if section
      render plain: section
    else
      logger.info("release notes requested for unknown version #{requested}")
      render plain: "Unknown version #{requested}", status: :not_found
    end
  end

  private

  def extract_section(notes, version)
    notes.split(/^## /).find { |chunk| chunk.start_with?("#{version}\n", "#{version} ") }
  end
end
