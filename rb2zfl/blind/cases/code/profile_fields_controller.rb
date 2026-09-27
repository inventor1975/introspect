class Profile
  PUBLIC_FIELDS = %w[display_name bio location website].freeze

  attr_reader :attributes

  def initialize(attributes)
    @attributes = attributes
  end
end

Profile.class_eval do
  Profile::PUBLIC_FIELDS.each do |field|
    define_method(field) { attributes[field] }
  end
end

class ProfileFieldsController < ApplicationController
  def show
    profile = Profile.new(params.fetch(:profile, {}).permit(*Profile::PUBLIC_FIELDS).to_h)
    field = params[:field]
    return head(:bad_request) unless Profile::PUBLIC_FIELDS.include?(field)
    render json: { field => profile.public_send(field) }
  end
end
