chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
         "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
         "Y", "Z"]

H_GROUP = "7"
Y_GROUP = "8"
VOWEL_GROUP = "0"

# Letter classes
codes = [VOWEL_GROUP, "1", "2", "3", VOWEL_GROUP, "1", "2", H_GROUP, VOWEL_GROUP,
         "2", "2", "4","5", "5", VOWEL_GROUP, "1", "2", "6", "2", "3", VOWEL_GROUP,
         "1", H_GROUP, "2", Y_GROUP, "2"]

# Vowels are divided into further groups based on their sound
vowel_1 = '#'
vowel_2 = '$'
vowel_3 = '%'
vowel_4 = '*'
vowel_5 = '^'

# Vowel classification
classification = {
    'A': vowel_1, 'AA': vowel_1, 'E': vowel_1, 'AI': vowel_1,
    'EE': vowel_2, 'I': vowel_2, 'Y': vowel_2,
    'U': vowel_3, 'OO': vowel_3, 'OU': vowel_3, 'AU': vowel_3,
    'O': vowel_4
}

VOWEL_TRUNCATION = 2

class ImprovedSoundex(object):
    """
    Improved Soundex is a heavily tricked out version of the traditional
    Soundex algorithm where vowels are also classified according to their
    sound.

    It also has custom rules for 2 groups known as Y_GROUP and H_GROUP which
    are ['Y'] and ['H', 'W'] respectively.
    """
    def _get_vowel_code(self, text):
        sequence = []
        code = classification.get(text, None)

        if code:
            return code

        prev = None
        for letter in text:
            if len(sequence) > 2:
                break

            if letter == prev:
                continue

            code = classification.get(letter, None)
            if code:
                sequence.append(code)

            prev = letter

        return ''.join(sequence) if sequence else None

    def soundex_code(self, text):
        code_sequence = []
        vowels = []

        for letter in text.upper():
            try:
                code = codes[chars.index(letter)]
            except ValueError:
                continue

            if code == Y_GROUP:
                # Consider 'Y' as vowel if previous is consonant
                if not vowels:
                    code = VOWEL_GROUP

            if code == VOWEL_GROUP:
                vowels.append(letter)
                continue

            if code == H_GROUP:
                # Add 'H' to code_sequence if previous is a vowel
                if not vowels:
                    continue

            if vowels:
                # Truncate vowels to length of VOWEL_TRUNCATION
                vowel_string = ''.join(vowels[:VOWEL_TRUNCATION])
                code_sequence.append(self._get_vowel_code(vowel_string))
                vowels = []

            code_sequence.append(code)

        # Handle the vowels at the end of the word
        if vowels:
            # Truncate vowels to length of VOWEL_TRUNCATION
            vowel_string = ''.join(vowels[:VOWEL_TRUNCATION])
            code_sequence.append(self._get_vowel_code(vowel_string))

        # Remove all 'H's in the end
        while code_sequence[-1] == H_GROUP:
            code_sequence = code_sequence[:-1]

        code_string = ''
        prev = ''
        # Convert the code_sequence `list` to a string
        for char in code_sequence:
            if char == prev or char is None:
                continue
            code_string += char
            prev = char

        return code_string

    def compare(self, ying, yang):
        return self.soundex_code(ying) == self.soundex_code(yang)

