module DocsHelper
  DOC_ROOT = Rails.root.join("app", "views", "docs", "articles").to_s

  def current_doc_title
    params[:doc].to_s.tr("_", " ").capitalize
  end

  def current_doc_body
    source = File.read(File.join(DOC_ROOT, params[:doc].to_s))
    simple_format(source)
  end
end
