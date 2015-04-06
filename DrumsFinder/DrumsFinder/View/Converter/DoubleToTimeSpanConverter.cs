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
    [ValueConversion(typeof(Double), typeof(TimeSpan))]
    class DoubleToTimeSpanConverter : IValueConverter
    {
        #region IValueConverter Members


        #endregion
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            if (value != null)
                return ((TimeSpan)value).TotalSeconds;
            else
                return 0;
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            return new TimeSpan((long)((Double)value) * 10000000);

        }
    }
}
