def clean(x)
  x.strip
end
def run
  system("ls " + clean(params[:c]))   # REFUTED (implicit return)
end
