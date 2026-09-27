class Vendor < ApplicationRecord
  def self.catalog_for(params)
    country = params[:country]
    find_by_sql("SELECT * FROM vendors WHERE country_code = '#{country}' AND active = 1")
  end
end
