


# TODO: possibly use more than one example, or more than one encoding
# TODO: remove extraneous print statements in examples?


def ex01():
    # This example extracts first a part, then a measure from a complete score. Next, pitches are isolated from this score as pitch classes. Finally, consecutive pitches from this measure are extracted, made into a chord, and shown to be a dominant seventh chord. 
    
    from music21 import corpus, chord
    sStream = corpus.parseWork('opus133.xml') # load a MusicXML file
    v2Part = sStream[1].measures # get all measures from the second violin
    v2Part[48].show() # render the 48th measure as notation
    
    # create a list of pitch classes in this measure
    pcGroup = [n.pitchClass for n in v2Part[48].pitches] 
    print pcGroup # display the collected pitch classes as a list
    # extract from the third pitch until just before the end
    pnGroup = [n.nameWithOctave for n in v2Part[48].pitches[2:-1]] 
    qChord = chord.Chord(pnGroup) # create a chord from these pitches
    qChord.show() # render this chord as notation
    print qChord.isDominantSeventh() # find if this chord is a dominant
    



def ex02():

    
    # This example searches the second violin part for adjacent non-redundant pitch classes that form dominant seventh chords.
    
    from music21 import corpus, chord, stream
    
    sStream = corpus.parseWork('opus133.xml') # load a MusicXML file
    v2Part = sStream[1].measures # get all measures from the first violin
    
    # First, collect all non-redundant adjacent pitch classes, and store these pitch classes in a list. 
    pitches = []
    for i in range(len(v2Part.pitches)):
        pn = v2Part.pitches[i].name
        if i > 0 and pitches[-1] == pn: continue
        else: pitches.append(pn)
    
    # Second, compare all adjacent four-note groups of pitch classes and determine which are dominant sevenths; store this in a list and display the results. 
    found = stream.Stream()
    for i in range(len(pitches)-3):
        testChord = chord.Chord(pitches[i:i+4])
        if testChord.isDominantSeventh():
            found.append(testChord)
    found.show()
    
   

def ex03():
    
    # This examples graphs the usage of pitch classes in the first and second violin parts. 
    
    from music21 import corpus
    from music21.analysis import correlate
    sStream = corpus.parseWork('opus133.xml') # load a MusicXML file
    # Create a graph of pitch class for the first and second part
    for part in [sStream[0], sStream[1]]:
        na = correlate.NoteAnalysis(part.flat)
        fx = lambda n: n.pitchClass # x values will be pitch classes
        fxTick = lambda n: n.name # x ticks will be pitch names
        na.noteAttributeHistogram(fx, title=part.getInstrument().partName,
                                  fxTick=fxTick)
    



def ex04():
    
    # This example, by graphing pitch class over note offset, shows the usage of pitch classes in the violoncello part over the duration of the composition. While the display is coarse, it is clear that the part gets less chromatic towards the end of the work.
    
    from music21 import corpus
    from music21.analysis import correlate
    sStream = corpus.parseWork('opus133.xml') # load a MusicXML file
    na = correlate.NoteAnalysis(sStream[3].flat)
    fy = lambda n: n.pitchClass # y values will be pitch classes
    fx = lambda n: n.offset # x values will be offsets in quarter notes
    na.noteAttributeScatter(fx, fy, yTicks=correlate.ticksPitchClass())






#-------------------------------------------------------------------------------

def ex01Alt():
    # measure here is a good test of dynamics positioning:
    from music21 import corpus, chord
    sStream = corpus.parseWork('opus133.xml') # load a MusicXML file
    v2Part = sStream[1].measures # get all measures from the second violin
    v2Part[45].show() # render the 48th measure as notation



def findHighestNotes():
    import copy
    import music21
    from music21 import corpus, meter, stream
    
    score = corpus.parseWork('bach/bwv366.xml')
    ts = score.flat.getElementsByClass(meter.TimeSignature)[0]
    ts.beat.partition(3)
    
    found = stream.Stream()
    for part in score:
        found.append(part.flat.getElementsByClass(music21.clef.Clef)[0])
        highestNoteNum = 0
        for m in part.measures:
            for n in m.notes:
                if n.midi > highestNoteNum:
                    highestNoteNum = n.midi
                    highestNote = copy.deepcopy(n) # optional
    
                    # These two lines will keep the look of the original
                    # note values but make each note 1 4/4 measure long:
    
                    highestNote.duration.components[0].unlink()
                    highestNote.quarterLength = 4
                    highestNote.lyric = '%s: M. %s: beat %s' % (
                        part.getInstrument().partName[0], m.measureNumber, ts.getBeat(n.offset))
        found.append(highestNote)

    print found.write('musicxml')


from music21 import *

def ex1_revised():
    beethovenScore = corpus.parseWork('beethoven/opus133.xml') 
    violin2 = beethovenScore[1]      # most programming languages start counting from 0, 
    #  so part 0 = violin 1, part 1 = violin 2, etc.
    display = stream.Stream() # an empty container for filling with found notes
    for thisMeasure in violin2.measures:
        notes = thisMeasure.findConsecutiveNotes(skipUnisons = True, skipChords = True,
                       skipOctaves = True, skipRests = True, noNone = True )
        pitches = [n.pitch for n in notes]
        for i in range(len(pitches) - 3):
            testChord = chord.Chord(pitches[i:i+4])
            testChord.duration.type = "whole"
            if testChord.isDominantSeventh() is True:
                # since a chord was found in this measure, append the found pitches in closed position
                testChord.lyric = "m. " + str(thisMeasure.measureNumber)
                emptyMeasure = stream.Measure()
                emptyMeasure.append(testChord.closedPosition())
                display.append(emptyMeasure)
    
                # append the whole measure as well, tagging the first note of the measure with an
                # ordered list of all the pitch classes used in the measure.
                pcGroup = [p.pitchClass for p in thisMeasure.pitches]
                firstNote = thisMeasure.getElementsByClass(note.Note)[0]
                firstNote.lyric = str(sorted(set(pcGroup)))
                thisMeasure.setRightBarline("double")
                display.append(thisMeasure)
    
    display.show('musicxml')

ex1_revised()