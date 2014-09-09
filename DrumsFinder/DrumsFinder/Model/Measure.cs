using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class Measure
    {
        public ObservableCollection<Note> Notes { get; set; }
        public ObservableCollection<Note> Independance { get; set; }

        public int UpperTimeSig { get; set; }
        public int LowerTimeSig { get; set; }

        public Measure()
        {
            UpperTimeSig = 4;
            LowerTimeSig = 4;

            Notes = new ObservableCollection<Note>();
            Independance = new ObservableCollection<Note>();
            Notes.Add(new Note(NoteKind.Kick, NoteDuration.Whole));
            Notes.Add(new Note(NoteKind.Snare, NoteDuration.Quartet));
            Notes.Add(new Note(NoteKind.Kick, NoteDuration.Quartet));
            Notes.Add(new Note(NoteKind.Snare, NoteDuration.Quartet));
         
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
            //Independance.Add(new Note(NoteKind.Charley, NoteDuration.eighth));
        }

        public double GetLength()
        {
            return Notes.Sum(item => 1 / (double)item.Duration);
        }

        public double GetActualLength()
        {
            return UpperTimeSig * (1 / (double)LowerTimeSig);
        }
    }
}
