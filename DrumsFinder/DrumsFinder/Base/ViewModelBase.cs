using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DrumsFinder.Base
{
    //Puisque toutes les classes Vue-Modèle doivent implémenter l'interface INotifyPropertyChanged, ce travail peut n'être fait qu'une fois, en définissant une classe de base dont toutes les classes Vue- Modèle dériveront. 
    //J'ai l'habitude pour cela d'écrire une méthode protégée OnPropertyChanged qui attend en argument le nom de la propriété qui a changée, et qui lève l'événement PropertyChanged associé.
    public abstract class ViewModelBase : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            var handler = PropertyChanged;

            if (handler != null)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
}
