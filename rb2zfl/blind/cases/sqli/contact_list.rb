class ContactListController < ApplicationController
  def index
    name = params[:name]
    @contacts = ActiveRecord::Base.connection.exec_query(
      "SELECT id, name, phone FROM contacts WHERE name = $1",
      "contacts_by_name",
      [name]
    ).to_a
    render json: @contacts
  end
end
