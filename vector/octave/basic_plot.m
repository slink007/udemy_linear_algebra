% 3-dimensional row vector
v3 = [ 4 -3 2 ];

% the main plotting code:
plot3([0 v3(1)],[0 v3(2)],[0 v3(3)],'linew',2)

% make the plot look nicer
axis square
axis([ -4 4 -4 4 -4 4 ])
hold on, grid on
plot3(get(gca,'xlim'),[0 0],[0 0],'k--')
plot3([0 0],get(gca,'ylim'),[0 0],'k--')
plot3([0 0],[0 0],get(gca,'zlim'),'k--')
xlabel('X_1 dimension')
ylabel('X_2 dimension')
zlabel('X_3 dimension')

% might be easier to see when rotated
rotate3d on
