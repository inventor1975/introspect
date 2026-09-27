class Admin::CustomFieldsController < ApplicationController
  def create
    name = params[:field][:name]
    default = params[:field][:default]

    Contact.module_eval <<~RUBY, __FILE__, __LINE__ + 1
      def #{name}
        custom_data.fetch("#{name}", #{default.inspect})
      end
    RUBY

    CustomField.create!(name: name, default_value: default)
    redirect_to admin_custom_fields_path
  end
end
