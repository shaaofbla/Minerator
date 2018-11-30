from mido import MidiFile, MidiTrack

def collectNoteMessages(midi):
    NoteMessages = []
    for track in midi.tracks:
        for msg in track:
            if (msg.type == "note_on" or msg.type == "note_off"):
                NoteMessages.append(msg)
    return NoteMessages

def loadMidiFile(midiFile):
    midi = MidiFile(midiFile)
    return midi

def collectMetaMessages(midiTrack, newTrack):
    for msg in midiTrack:
        if (msg.is_meta):
            print "msg", msg.type
            if msg.type != "end_of_track":
                newTrack.append(msg)
            else:
                endOfTrackMsg = msg
    return newTrack, endOfTrackMsg

def collectModelMetaMessages(midi):
    metaMessages = MidiFile()
    endOfTrack= []
    for track in midi.tracks:
        newTrack = MidiTrack()
        newTrack, endOfTrackMsg = collectMetaMessages(track, newTrack)
        metaMessages.tracks.append(newTrack)
        endOfTrack.append(endOfTrackMsg)
    return metaMessages, endOfTrack

def setFirstNoteToTimePointZero(notes):
    notes[0].time = 0
    return notes

def newMidiFileWithoutPrimer(primerNotes, modelNotes, modelMetaMessages):
    chopped_midi = modelMetaMessages
    chopped_notes = modelNotes[len(primerNotes)+1:-1]
    chopped_notes = setFirstNoteToTimePointZero(chopped_notes)
    for i in range(len(chopped_notes)):
        chopped_midi.tracks[1].append(chopped_notes[i])
    return chopped_midi

def readTrack(midiFile, track):
    midi = MidiFile(midiFile)
    miditrack = midi.tracks[track]
    if len(miditrack) == 0:
        raise RuntimeError("readTrack: Midi track doesn't contain any notes.")

def addEndOfTracks(midi, endofTracks):
    if (len(midi.tracks) != len(endofTracks)):
        raise RuntimeError("addEndOfTracks: both lists must be of same length.")
    else:
        for i in range(len(midi.tracks)):
            midi.tracks[i].append(endofTracks[i])
    return midi

def chopPrimer(primer, modelOutput):
    modelMidi = MidiFile(modelOutput)
    primerMidi = MidiFile(primer)
    model = readTrack(modelOutput, 1)
    metaMessages, endOfTrack = collectModelMetaMessages(modelMidi)
    primerNotes = collectNoteMessages(primerMidi)
    modelNotes = collectNoteMessages(modelMidi)
    choppedMidi = newMidiFileWithoutPrimer(primerNotes, modelNotes, metaMessages)
    choppedMidi.ticks_per_beat = modelMidi.ticks_per_beat
    choppedMidi = addEndOfTracks(choppedMidi, endOfTrack)
    return choppedMidi