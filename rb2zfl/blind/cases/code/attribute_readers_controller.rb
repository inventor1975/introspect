class Setting
  def initialize(store)
    @store = store
  end
end

class AttributeReadersController < ApplicationController
  NAME_FORMAT = /\A[a-z][a-z0-9_]{0,31}\z/

  def create
    name = params[:name].to_s
    return head(:unprocessable_entity) unless NAME_FORMAT.match?(name)

    Setting.class_eval("def #{name}; @store.fetch(#{name.to_sym.inspect}, nil); end")
    head :created
  end
end
