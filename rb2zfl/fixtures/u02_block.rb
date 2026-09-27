def run
  params[:files].each do |f|
    system("cat " + f)                # REFUTED (inside a block)
  end
end
