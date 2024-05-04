class TextType:
    Text = 0,
    Bold = 1,
    Italic = 2,
    Code = 3,
    Link = 4,
    Image = 5,
    
    def get_all_types():
        return [TextType.Text, TextType.Bold, TextType.Italic, TextType.Code, TextType.Link, TextType.Image]
    
    def get_all_text_types():
        return [TextType.Text, TextType.Bold, TextType.Italic, TextType.Code]
    
    def is_more_than(text_type_1, text_type_2):
        return text_type_1 > text_type_2
    
    def is_less_than(text_type_1, text_type_2):
        return text_type_1 < text_type_2
    
    def is_equal(text_type_1, text_type_2):
        return text_type_1 == text_type_2
    
    
class BlockType:
    Paragraph = 0,
    Heading = 1,
    Code = 2,
    Quote = 3,
    UnorderedList = 4,
    OrderList = 5,
    
    def get_all_types():
        return [BlockType.Paragraph, BlockType.List, BlockType.Quote, BlockType.Code, BlockType.Heading]
    
    def is_more_than(block_type_1, block_type_2):
        return block_type_1 > block_type_2
    
    def is_less_than(block_type_1, block_type_2):
        return block_type_1 < block_type_2
    
    def is_equal(block_type_1, block_type_2):
        return block_type_1 == block_type_2