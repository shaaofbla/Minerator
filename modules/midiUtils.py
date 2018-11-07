from mido import MidiFile, MidiTrack

def collectNoteMessages(midiTrack):
    NoteMessages = []
    for msg in midiTrack:
        if (msg.type == "note_on" or msg.type == "note_off"):
            NoteMessages.append(msg)
    return NoteMessages

def collectMetaMessages(midiTrack):
    metaMessages = []
    for msg in midiTrack:
        if (msg.is_meta):
            metaMessages.append(msg)
    return metaMessages

def setFirstNoteToTimePointZero(notes):
    notes[0].time = 0
    return notes

def newMidiFileWithoutPrimer(notesOne, notesTwo, MetaMessages):
    chopped_midi = MidiFile()
    track = MidiTrack()
    chopped_midi.tracks.append(track)

    for metaMsg in MetaMessages:
        track.append(metaMsg)

    chopped_notes = notesTwo[len(notesOne):-1]
    chopped_notes = setFirstNoteToTimePointZero(chopped_notes)

    for i in range(len(chopped_notes)):
        track.append(chopped_notes[i])
    return chopped_midi

def chopPrimer(primer, modelOutput):
    primerMidi = MidiFile(primer)
    primer = primerMidi.tracks[0]
    midi = MidiFile(modelOutput)
    model = midi.tracks[1]
    metaMessages = collectMetaMessages(midi.tracks[0])
    primerNotes = collectNoteMessages(primer)
    modelNotes = collectNoteMessages(model)
    choppedMidi = newMidiFileWithoutPrimer(primerNotes, modelNotes, metaMessages)
    choppedMidi.ticks_per_beat = midi.ticks_per_beat
    return choppedMidi
    #createDir(root.saveDir)
    #choppedMidi.save("{}/test.mid".format(root.saveDir))