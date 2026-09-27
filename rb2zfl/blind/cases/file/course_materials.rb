require "sinatra/base"

class CourseMaterials < Sinatra::Base
  MATERIAL_DIR = "/srv/courses/materials".freeze
  MATERIALS = %w[week1.pdf week2.pdf week3.pdf syllabus.pdf].freeze

  helpers do
    def allowed_material?(name)
      MATERIALS.include?(name)
    end
  end

  get "/materials" do
    name = params[:m]
    halt 404 unless allowed_material?(name)

    send_file File.join(MATERIAL_DIR, name)
  end
end
