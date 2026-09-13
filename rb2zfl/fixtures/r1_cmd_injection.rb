class UsersController
  def ping
    host = params[:host]
    system("ping -c1 #{host}")      # EXPECT: REFUTED [shell]
  end
end
