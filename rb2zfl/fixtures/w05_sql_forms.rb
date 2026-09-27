class Item < ApplicationRecord
  def self.search(params)
    find_by_sql("SELECT * FROM items WHERE name LIKE '%#{params[:q]}%'") # implicit self
  end
end

class ItemsController < ApplicationController
  def index
    frag = "name = '#{params[:n]}'"
    Item.where(frag)
    Item.where(name: params[:n]) # a hash condition is bound
    ActiveRecord::Base.connection.exec_query("SELECT * FROM items WHERE id = $1", "q", [params[:id]])
  end
end
