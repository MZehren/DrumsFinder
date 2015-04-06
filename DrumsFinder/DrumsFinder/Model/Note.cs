using DrumsFinder.Base;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace DrumsFinder.Model
{
    [Flags]
    public enum NoteKind
    {
        Silence = 0,
        Kick = 1,
        Snare = 2,
        HighTom = 4,
        MedTom = 8,
        LowTom = 16,
        OpenHiHat = 32,
        ClosedHiHat = 64,
        Ride = 128,
        Crash = 256,
        China = 512
    };

    public enum NoteDuration
    {
        Whole = 1,
        Half = 2,
        Quartet = 4,
        Eighth = 8,
        Sixteenth = 16,
        ThirtySecond = 32
    };

    public enum TimeDivision
    {
        Binary = 1,
        Ternary
    };

    public class Note
    {
        private Measure _parent;
        public NoteKind Kind { get; set; }
        public NoteDuration Duration { get; set; }
        public Double Length
        {
            get
            {
                return 100 / (double)Duration;
            }
        }

        public bool Doted { get; set; }
        public TimeDivision Division { get; set; }

        //public double Length
        //{
        //    get
        //    {
        //        return Length / ((double)Tempo / (4 * 60));
        //    }
        //}

        public ICommand Play
        {
            get
            {
                return new RelayCommand(
                    delegate()
                    {
                        AudioPlayBack.AddSound(this.Kind);
                    });
            }
        }

        public Note(NoteKind Kind, NoteDuration Duration, Measure Parent)
        {
            this.Duration = Duration;
            this.Kind = Kind;
        }
    }
}
