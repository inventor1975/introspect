class FeedbackEntry
  attr_reader :author, :message

  def initialize(author:, message:)
    @author = author
    @message = message
  end

  def self.quote_block(text, author)
    "<blockquote><p>#{text}</p><footer>#{author}</footer></blockquote>"
  end

  def rendered
    self.class.quote_block(message, author)
  end
end
