#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <vector>
#include <queue>
#include <limits>
//g++ memory-x5.cpp -o memory-x
// ------------------------------------------------------
// We first define how many files we want for BFS
// We'll do BFS for file indices 0..99 => 100 files => 10,000 lines
// Then create file 100 as a special placeholders file.
// ------------------------------------------------------
static const int NUM_FILES_BFS = 100; // BFS from fileIndex=0..99
static const int LINES_PER_FILE = 100;
static const int TOTAL_BFS_STRINGS = NUM_FILES_BFS * LINES_PER_FILE; // 10,000

// We'll also define a special fileIndex=100 for <TAB>, <NEWLINE>, <WHITESPACE>
static const int FILE_INDEX_SPECIAL = 100; // the 101st file

// We'll load dictionary files from 0..100 => 101 files total
static const int MAX_FILE_INDEX = 100; // 0..100 inclusive

// ------------------------------------------------------
// The BFS ALPHABET (no literal '\n' or '\t', but includes ' ').
// We'll store placeholders for those in 100.txt
// ------------------------------------------------------
static const std::vector<char> ALPHABET = {
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    '0','1','2','3','4','5','6','7','8','9',
    ' ', // space
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '-', '_', '+', '=','{','}','[',']','|','\\',':',';','\"','\'','<','>',
    ',','.','?','/','`','~'
};

// BFS max length (e.g. up to 4)
static const int SAFE_MAX_LENGTH = 4;

// ------------------------------------------------------
// We'll store dictionary as:
// dictionary[fileIndex][wordIndex] = wordString
// ------------------------------------------------------
static std::map<int, std::map<int, std::string>> dictionary;

// ------------------------------------------------------
// Placeholders in 100.txt
// We'll interpret them at parse time as real tab/newline/space
// ------------------------------------------------------
static const std::string PLACEHOLDER_TAB        = "<TAB>";
static const std::string PLACEHOLDER_NEWLINE    = "<NEWLINE>";
static const std::string PLACEHOLDER_WHITESPACE = "<WHITESPACE>";

// ------------------------------------------------------
// 1) MODE 0: BFS for files 0..99 => 10,000 lines
//    Then create file 100 with placeholders. Then we load them all.
// ------------------------------------------------------
void generateBFSForFiles0to99()
{
    std::cout << "[Mode 0] Generating BFS dictionary files 0..99 ("
              << TOTAL_BFS_STRINGS << " tokens total)...\n";

    // BFS
    std::queue<std::string> q;
    for (char c : ALPHABET)
    {
        q.push(std::string(1, c));
    }

    std::vector<std::string> generated;
    generated.reserve(TOTAL_BFS_STRINGS);

    while (!q.empty() && (int)generated.size() < TOTAL_BFS_STRINGS)
    {
        std::string front = q.front();
        q.pop();
        generated.push_back(front);

        if ((int)front.size() < SAFE_MAX_LENGTH)
        {
            for (char c : ALPHABET)
            {
                q.push(front + c);
            }
        }
    }

    // Write them out to 0..99
    int globalIndex = 0;
    for (int fileIndex = 0; fileIndex < NUM_FILES_BFS; ++fileIndex)
    {
        std::string fname = std::to_string(fileIndex) + ".txt";
        std::ofstream out(fname);
        if (!out.is_open())
        {
            std::cerr << "[Warning] Could not open " << fname << " for writing.\n";
            continue;
        }
        out << fileIndex << " {\n";
        for (int lineIndex = 0; lineIndex < LINES_PER_FILE; ++lineIndex)
        {
            if (globalIndex >= (int)generated.size()) break;
            out << lineIndex << " " << generated[globalIndex] << "\n";
            globalIndex++;
        }
        out << "}\n";
        out.close();
    }
    std::cout << "[Mode 0] BFS wrote " << globalIndex << " lines (files 0..99).\n";
}

void createFile100withPlaceholders()
{
    // We'll create "100.txt" with lines:
    // 100 {
    //   0 <TAB>
    //   1 <NEWLINE>
    //   2 <WHITESPACE>
    // }
    const std::string fname = "100.txt";
    std::ofstream out(fname);
    if (!out.is_open())
    {
        std::cerr << "[Warning] Could not open 100.txt for writing.\n";
        return;
    }
    out << 100 << " {\n";
    out << 0 << " " << PLACEHOLDER_TAB << "\n";
    out << 1 << " " << PLACEHOLDER_NEWLINE << "\n";
    out << 2 << " " << PLACEHOLDER_WHITESPACE << "\n";
    out << "}\n";
    out.close();

    std::cout << "[Mode 0] Created 100.txt with <TAB>, <NEWLINE>, <WHITESPACE>.\n";
}

void generateAllDictionaryFilesAndLoad()
{
    // BFS for 0..99
    generateBFSForFiles0to99();
    // Create 100.txt
    createFile100withPlaceholders();

    // Now load from 0..100 => 101 files total
    dictionary.clear();
    bool success = true;
    for (int i = 0; i <= MAX_FILE_INDEX; ++i)
    {
        std::string fname = std::to_string(i) + ".txt";
        std::ifstream inFile(fname);
        if (!inFile.is_open())
        {
            std::cerr << "[Warning] Could not open " << fname << "\n";
            success = false;
            continue;
        }
        bool foundBrace = false;
        std::string line;
        // skip until '{'
        while (std::getline(inFile, line))
        {
            if (line.find('{') != std::string::npos)
            {
                foundBrace = true;
                break;
            }
        }
        if (!foundBrace)
        {
            std::cerr << "[Warning] No '{' in " << fname << "\n";
            success = false;
            continue;
        }

        // read lines until '}'
        while (std::getline(inFile, line))
        {
            if (line.find('}') != std::string::npos) break;
            if (line.empty()) continue;

            std::stringstream ss(line);
            int wIndex;
            if (!(ss >> wIndex))
            {
                std::cerr << "[Warning] parse error in " << fname << ": " << line << "\n";
                continue;
            }
            std::string token;
            if (!std::getline(ss, token)) continue;
            // trim leading spaces
            while (!token.empty() && (token.front()==' '||token.front()=='\t'))
                token.erase(token.begin());

            // unescape if placeholders
            if (token == PLACEHOLDER_TAB)        token = "\t";
            else if (token == PLACEHOLDER_NEWLINE) token = "\n";
            else if (token == PLACEHOLDER_WHITESPACE) token = " ";

            dictionary[i][wIndex] = token;
        }
    }

    if (success)
    {
        std::cout << "[Mode 0] Dictionary files loaded (0..100). We now have BFS + placeholders.\n";
    }
    else
    {
        std::cerr << "[Warning] Some dictionary files could not be loaded.\n";
    }
}

// ------------------------------------------------------
// findWordInDictionaryDescending: scan from file 100 down to 0
// so file 100 has priority if the same token is repeated
// (since you specifically asked for descending order).
// ------------------------------------------------------
bool findWordInDictionaryDescending(const std::string &word,
                                    int &outFileIndex, int &outWordIndex)
{
    // note: we must do i from 100..0
    for (int i = MAX_FILE_INDEX; i >= 0; --i)
    {
        auto itFile = dictionary.find(i);
        if (itFile == dictionary.end()) continue;
        for (auto &pr : itFile->second)
        {
            if (pr.second == word)
            {
                outFileIndex = i;
                outWordIndex = pr.first;
                return true;
            }
        }
    }
    return false;
}

// ------------------------------------------------------
// Encode piecewise: parse user input from left->right, 
// for each position try largest substring (desc file order).
// Produce triple-dot codes (#.0.#).
// ------------------------------------------------------
std::string encodeStringPiecewise(const std::string &input)
{
    std::string result;
    size_t pos = 0;
    while (pos < input.size())
    {
        bool found = false;
        for (size_t length = input.size()-pos; length>0; --length)
        {
            std::string candidate = input.substr(pos, length);
            int fIdx, wIdx;
            if (findWordInDictionaryDescending(candidate, fIdx, wIdx))
            {
                if (!result.empty()) result += " ";
                result += std::to_string(fIdx) + ".0." + std::to_string(wIdx);
                pos += length;
                found = true;
                break;
            }
        }
        if (!found)
        {
            std::cerr << "[Warn] No match at pos=" << pos 
                      << " (char='" << input[pos] << "'). Skipping.\n";
            pos++;
        }
    }
    return result;
}

// ------------------------------------------------------
// Decode triple-dot #.0.# => direct dictionary lookup
// no extra spaces inserted. 
// ------------------------------------------------------
std::string decodeCodeToString(const std::string &codeSequence)
{
    std::stringstream ss(codeSequence);
    std::string token;
    std::string output;

    while (ss >> token)
    {
        // parse X.0.Y
        size_t dot1 = token.find('.');
        if (dot1 == std::string::npos)
        {
            std::cerr << "[Warning] invalid token (no dot): " << token << "\n";
            continue;
        }
        size_t dot2 = token.find('.', dot1+1);
        if (dot2 == std::string::npos)
        {
            std::cerr << "[Warning] invalid token (only one dot): " << token << "\n";
            continue;
        }
        if (token.find('.', dot2+1) != std::string::npos)
        {
            std::cerr << "[Warning] invalid token (more than 2 dots): " << token << "\n";
            continue;
        }

        std::string sFileIndex = token.substr(0, dot1);
        std::string sMid       = token.substr(dot1+1, dot2 - (dot1+1));
        std::string sWordIndex = token.substr(dot2+1);

        if (sMid != "0")
        {
            std::cerr << "[Warning] middle segment not '0': " << token << "\n";
            continue;
        }
        int fileIndex, wordIndex;
        try {
            fileIndex = std::stoi(sFileIndex);
            wordIndex = std::stoi(sWordIndex);
        } catch(...) {
            std::cerr << "[Warning] parse error: " << token << "\n";
            continue;
        }

        auto itFile = dictionary.find(fileIndex);
        if (itFile == dictionary.end())
        {
            std::cerr << "[Warning] fileIndex " << fileIndex << " not found.\n";
            continue;
        }
        auto &inner = itFile->second;
        auto wit = inner.find(wordIndex);
        if (wit == inner.end())
        {
            std::cerr << "[Warning] wordIndex " << wordIndex 
                      << " not found in file " << fileIndex << "\n";
            continue;
        }

        // append directly
        output += wit->second;
    }
    return output;
}

// ------------------------------------------------------
// MAIN with 5 modes:
// 0 -> BFS for 0..99, create 100 with placeholders, load 0..100
// 1 -> encode piecewise
// 2 -> decode triple-dot
// 3 -> save last result
// 4 -> exit
// ------------------------------------------------------
int main()
{
    bool running = true;
    std::string lastResult;

    while (running)
    {
        std::cout << "\n==== MENU ====\n";
        std::cout << "0) Generate BFS (0..99) + placeholders (100) and Load\n";
        std::cout << "1) Encode piecewise\n";
        std::cout << "2) Decode triple-dot code\n";
        std::cout << "3) Save last result\n";
        std::cout << "4) Exit\n";
        std::cout << "Choose: ";

        int choice;
        std::cin >> choice;
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        switch(choice)
        {
        case 0:
        {
            generateAllDictionaryFilesAndLoad();
            break;
        }
        case 1:
        {
            if (dictionary.empty())
            {
                std::cout << "[Info] Dictionary empty. Generate or load first.\n";
                break;
            }
            std::cout << "Enter multi-line string (finish with blank line):\n";
            std::string inputLines, temp;
            while (true)
            {
                if(!std::getline(std::cin, temp)) break; // EOF
                if(temp.empty()) break; 
                if(!inputLines.empty()) inputLines += "\n";
                inputLines += temp;
            }
            std::string code = encodeStringPiecewise(inputLines);
            std::cout << "\nEncoded code:\n" << code << "\n";
            lastResult = code;
            break;
        }
        case 2:
        {
            if (dictionary.empty())
            {
                std::cout << "[Info] Dictionary empty. Generate or load first.\n";
                break;
            }
            std::cout << "Enter triple-dot code sequence:\n";
            std::string codeSeq;
            std::getline(std::cin, codeSeq);
            std::string decoded = decodeCodeToString(codeSeq);
            std::cout << "\nDecoded string:\n" << decoded << "\n";
            lastResult = decoded;
            break;
        }
        case 3:
        {
            if (lastResult.empty())
            {
                std::cout << "[Info] Nothing to save.\n";
                break;
            }
            std::cout << "Enter filename to save:\n";
            std::string fname;
            std::getline(std::cin, fname);

            std::ofstream out(fname);
            if (!out.is_open())
            {
                std::cerr << "[Error] Could not open " << fname << "\n";
                break;
            }
            out << lastResult << "\n";
            out.close();
            std::cout << "[Info] Saved last result to " << fname << "\n";
            break;
        }
        case 4:
            running = false;
            break;
        default:
            std::cout << "[Error] Invalid choice.\n";
            break;
        }
    }

    std::cout << "Exiting.\n";
    return 0;
}
