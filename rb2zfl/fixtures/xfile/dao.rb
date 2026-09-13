class Dao
  def q(id)
    User.find_by_sql("SELECT * FROM users WHERE id = #{id}")  # id -> sql
  end
end
