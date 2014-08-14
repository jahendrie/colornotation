#!/usr/bin/env python
#===============================================================================
#   colornotation.py    |   version 1.01    |   zlib license    |   2014-08-14
#   James Hendrie       |   hendrie.james@gmail.com
#===============================================================================
import sys
import getopt

options = { "stripHTML" : False, "writeList" : False }


#===============================================================================
#                                  PRINT HELP
#===============================================================================
def print_help():
    """
    Prints the help text
    """
    helpText ="""Usage:  colornotation.py [OPTIONS] [ITEMS]

This script is meant to be used in conjunction with the 'color note' app for
Android devices (as well as possibly other devices, I don't know).  To be
more specific, it's meant to make generating lists of stuff for that app
much easier than would otherwise be the case.  For instance, you can pipe
a directory listing to this script and redirect the output to an html file,
then send it to your phone for whatever degenerate purposes you wish.

Options:
    -h or --help:   This text
    --version:      Version and author info
    -t or --title:  The title of your note (default "Untitled Note")
    -l or --list:   Format the resultant HTML as a list
    -i or --input:  Select input file (default STDIN)
    -o or --output: Select output file (default STDOUT)
    -s or --strip:  Strip HTML from note, leaving plain text

Examples:
    ls ~/music | ./colornotation.py -l -t "Music List" > mlist.html
    ./colornotation.py --list -i list.txt -o list.html --title="Shopping"
    cat ~/docs/article.txt | ./colornotation.py > article.html
        """

    print( helpText )


#===============================================================================
#                                PRINT VERSION
#===============================================================================
def print_version():
    """
    Prints the version and author info
    """
    print( "colornotation.py, version 1.01" )
    print( "James Hendrie <hendrie.james@gmail.com>" )


#===============================================================================
#                                 WRITE HEADER
#===============================================================================
def write_header( title, outfile ):
    """
    This function writes the header at the top of the file; this is written
    prior to any of the list items.

    Args:
        title       The title of the list
        outfile     Points to the file we're writing to; most likely stdout
    """

    ##  Write all of the header stuff
    outfile.write( "<html><head>" )
    outfile.write( '<meta http-equiv="Content-Type" ' )
    outfile.write( 'content="text/html;charset=UTF-8"/>' )
    outfile.write( '<title>%s</title></head><body><p dir="ltr">' % title )


#===============================================================================
#                                 WRITE FOOTER
#===============================================================================
def write_footer( outfile ):
    """
    This function writes the footer at the end of the file, closing the list.

    Args:
        outfile     Points to the file we're writing to; most likely stdout
    """

    ##  Close out the file
    outfile.write( "</p>\n</body></html>" )


#===============================================================================
#                               WRITE LIST ITEMS
#===============================================================================
def write_list_items( items, outfile ):
    """
    This function writes the actual items passed to the program to the list.  A
    small amount of formatting is applied so that the list will show up properly
    in the app

    Args:
        items       List of stuff to be written
        outfile     Points to the file we're writing to; most likely stdout
    """

    ##  Write items with list formatting applied
    for i in items:
        outfile.write( "[ ] %s<br>\n" % i )



#===============================================================================
#                               WRITE NOTE TEXT
#===============================================================================
def write_note_text( items, outfile ):
    """
    This just prints whatever was given to the outfile, no special formatting.

    Args:
        items       A list of items to be written (text)
        outfile     Where we dump the output
    """

    ##  Write items without list formatting
    for i in items:
        outfile.write( i )


#===============================================================================
#                                  WRITE NOTE
#===============================================================================
def write_note( title, items, outfile ):
    """
    Master note-writing function; determines whether to write list items or
    regular note items (text).  Also calls the functions to write the header and
    the footer.

    Args:
        title       Title of the note (if any)
        items       Text to be written
        outfile     File to which we write
        writeList   Whether or not we're writing a list
    """

    ##  Write the header
    write_header( title, outfile )

    ##  Write the list / note
    if( options[ "writeList" ] == True ):
        write_list_items( items, outfile )
    else:
        write_note_text( items, outfile )

    ##  Write the footer, closing out the note
    write_footer( outfile )


#===============================================================================
#                                 HANDLE ARGS
#===============================================================================
def handle_args():
    """
    This function handles argument checking for the script.

    Returns:
        title       Title of the note (if any)
        args        Args left over after getopt is through checking
        infile      Where we get our input
        outfile     Where we stick our output
    """

    ##  Default title
    title = "Untitled Note"

    infile = sys.stdin
    outfile = sys.stdout

    ##  Get the opts:optargs and leftover arguments to the script
    opts, args = getopt.getopt(
            sys.argv[1:],
            "hlst:i:o:",
            ["help", "version", "list", "strip", "title=", "input=", "output="])

    ##  Go through the options and take appropriate action
    for opt, arg in opts:

        ##  If they want help
        if( opt == "-h" ) or ( opt == "--help" ):
            print_help()
            sys.exit( 0 )

        ##  Print author and version info
        if( opt == "--version" ):
            print_version()
            sys.exit( 0 )

        ##  If they're writing a list
        if( opt == "-l" ) or ( opt == "--list" ):
            options[ "writeList" ] = True

        ##  The title of the note
        if( opt == "-t" ) or ( opt == "--title" ):
            title = arg

        ##  User-specified input
        if( opt == "-i" ) or ( opt == "--input" ):
            try:
                infile = open( arg, "r" )
            except IOError:
                print("ERROR:  Cannot open %s for reading" % arg )
                sys.exit(1)

        ##  User-specified output
        if( opt == "-o" ) or ( opt == "--output" ):
            try:
                outfile = open( arg, "w" )
            except IOError:
                print("ERROR:  Cannot open %s for writing" % arg )
                sys.exit(1)

        ##  If the user wants to strip HTML
        if( opt == "-s" ) or ( opt == "--strip" ):
            options[ "stripHTML" ] = True

    ##  Return our things
    return( title, args, infile, outfile )



#===============================================================================
#                                  STRIP NOTE
#===============================================================================
def strip_note( infile, outfile ):
    """
    This function assumes that a colornote file is either being directly fed to
    the script or having its text piped in from the terminal.  Ruining other
    input is not our problem here.

    Args:
        infile      Where we're getting our input
        outfile     Where we put our output
    """

    ##  Grab the text
    text = infile.readlines()

    ##  I know that this isn't the fastest or most efficient way to do this, but
    ##  to be honest, I just like how it looks a lot better
    finalText = []

    ##  Get the first bit of text from the file, add to the text to be written
    saveme = text[ 0 ].partition( '<p dir="ltr">' )[2]
    finalText.append( saveme )

    ##  Add the rest of the text
    for t in text[ 1:-1 ]:
        finalText.append( t )

    ##  Go through the text, trimming list formatting if the user wants to and
    ##  printing the resultant text to the outfile (STDOUT by default)
    for t in finalText[0:-1]:
        ##  If indeed we give a shit about removing list stuff
        if( options[ "writeList" ] == True ):
            ##  Unchecked
            if( "[ ] " in t ):
                t = t.partition( "[ ] ")[2]
            ##  Checked
            elif( "[V] " in t ):
                t = t.partition( "[V] ")[2]

        ##  Write everything to the outfile
        outfile.write( "%s\n" % t[ 0:-5 ] )


#===============================================================================
#                                     MAIN
#===============================================================================
def main():
    """
    This script exists as an aid to the 'color note' app for Android (possibly
    for other mobile OSes as well, I couldn't say).  It lets a person using a
    computer, with relative ease, compile a note from terminal input.  It's good
    if you want to send a directory listout as a checklist to your phone, for
    instance.  Actually, that's specifically why this script exists, but I made
    it so that it can be used slightly differently as well, if you'd like.
    """

    ##  Process the args
    title, args, infile, outfile = handle_args()

    ##  Check if they're stripping HTML
    if( options[ "stripHTML" ] == True ):
        strip_note( infile, outfile )
        sys.exit( 0 )

    ##  No leftover args:  We assume stdin or user-specified input
    if( len( args ) == 0 ):
        items = []  ##  WE SHALL APPEND TO THIS PRESENTLY, mmmYes, mmmmm
        rawItems = infile.readlines()
        iLen = len( rawItems )
        for i in rawItems:
            #   We exclude the last character because we don't need the extra
            #   newline character in that position
            item = i[:-1]

            ##  We bother with 'iLen' because we don't want <br> after the last
            ##  item written to the list
            if( options[ "writeList" ] == False ) and iLen > 1:
                item += "<br>\n"
                iLen = iLen - 1

            items.append( item )

    ##  Extra args are processed as items to be added to the list/note
    else:
        items = args

    ##  Write the god-damned note
    write_note( title, items, outfile )



if __name__ == "__main__":
    main()
