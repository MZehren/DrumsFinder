using DrumsFinder.Base;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace DrumsFinder.Model
{
    public class Measure : ObservableObject
    {
        public ObservableCollection<Note> Notes { get; set; }
        public ObservableCollection<Note> Independance { get; set; }

        private int? _tempo;
        public int? Tempo
        {
            get
            {
                if (_tempo != null)
                    return _tempo;
                else
                    return _parent.Tempo;

            }
            set
            {
                if (value > 0 && value < 1000)
                    _tempo = value;
            }
        }

        private int _upperTimeSig, _lowerTimeSig;
        public string TimeSignature
        {
            get
            {
                return _upperTimeSig + "/" + _lowerTimeSig;
            }
            set
            {
                Regex rgx = new Regex("^[1-9][0-9]?/(1|2|4|8|16|32)$");

                if (rgx.IsMatch(value))
                {
                    string[] result = value.Split('/');
                    _upperTimeSig = int.Parse(result[0]);
                    _lowerTimeSig = int.Parse(result[1]);
                }
            }
        }

        public double Duration
        {
            get
            {
                double Length = _upperTimeSig * 1 / _lowerTimeSig;
                return Length / ((double)Tempo / (4 * 60));
            }
        }

        private Partition _parent;

        public Measure(Partition Parent)
        {
            Notes = new ObservableCollection<Note>();
            Independance = new ObservableCollection<Note>();
            Notes.Add(new Note(NoteKind.HighTom | NoteKind.OpenHiHat, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.LowTom, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.HighTom | NoteKind.OpenHiHat, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.LowTom, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.HighTom | NoteKind.OpenHiHat, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.LowTom, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.HighTom | NoteKind.OpenHiHat, NoteDuration.Eighth, this));
            Notes.Add(new Note(NoteKind.LowTom, NoteDuration.Eighth, this));

            this._parent = Parent;
            this.TimeSignature = "4/4";
        }

        public double GetLength()
        {
            return Notes.Sum(item => 1 / (double)item.Duration);
        }

    }
}
