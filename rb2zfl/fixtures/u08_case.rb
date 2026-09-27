def run
  c = "ls"
  case params[:m]
  when "a" then c = params[:c]
  when "b" then c = "pwd"
  end
  system(c)                           # REFUTED
end
