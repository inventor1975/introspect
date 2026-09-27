class PermissionMatrixController < ApplicationController
  KNOWN_SCOPES = %w[read write admin].freeze

  def index
    scope = params[:scope]
    scope = "read" unless KNOWN_SCOPES.include?(scope)
    @perms = Permission.find_by_sql(
      "SELECT * FROM permissions WHERE scope = '#{scope}'"
    )
    render json: @perms
  end
end
