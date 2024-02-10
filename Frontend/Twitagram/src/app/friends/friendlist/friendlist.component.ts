import { Component, OnInit } from '@angular/core';
import { FriendsService } from '../friends.service';

@Component({
  selector: 'app-friendlist',
  templateUrl: './friendlist.component.html',
  styleUrls: ['./friendlist.component.css']
})
export class FriendlistComponent implements OnInit {
  friendList: any[] = [];

  constructor(private friendService: FriendsService) { }

  ngOnInit(): void {
    this.getFriendList();
  }

  getFriendList(): void {
    this.friendService.getFriendList()
      .subscribe(response => {
        this.friendList = response.results;
      });
  }

  unfriendByUsername(friendUsername: string): void {
    this.friendService.unfriendByUsername(friendUsername).subscribe(
      () => {
        alert(`Are you sure`)
        console.log('Friend unfriended successfully');
        this.friendList = this.friendList.filter(friend => friend.friend !== friendUsername);
      },
      (error: any) => {
        console.error('Error unfriending friend:', error);
        
      }
    );
  }

}
