class UsersController
  def find
    name = params[:name]
    User.where("name = '#{name}'")  # EXPECT: REFUTED [sql]
  end
end
