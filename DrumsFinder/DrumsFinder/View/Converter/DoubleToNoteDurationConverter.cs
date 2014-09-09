using DrumsFinder.Model;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;

namespace DrumsFinder.View.Converter
{
    [ValueConversion(typeof(Double), typeof(NoteDuration))]
    class DoubleToNoteDurationConverter : IValueConverter
    {
        #region IValueConverter Members


        #endregion
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            if (value != null)
                return (int)value;
            else
                return 4;
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            return NoteDuration.Quartet;

        }
    }
}
