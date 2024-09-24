import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links


class TextExtractMarkdownElements(unittest.TestCase):
    def test_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_link_and_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])
        self.assertEqual(extract_markdown_links(text), [("to youtube", "https://www.youtube.com/@bootdotdev")])



if __name__ == "__main__":
    unittest.main()
